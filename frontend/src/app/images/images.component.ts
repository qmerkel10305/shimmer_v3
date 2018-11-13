import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ImagesService } from './images.service';

import { Point } from 'types/point';
import { Image } from 'types/image';
import { TargetRegion } from 'types/targetRegion';

import { TargetClassifierComponent } from './target-classifier/target-classifier.component';
import { Target } from 'types/target';

@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.css']
})
export class ImagesComponent implements AfterViewInit {
  static readonly MIN_SELECTION_SIZE = 0.1;

  private imageElement: HTMLImageElement;
  private context: CanvasRenderingContext2D;

  private locked: boolean;
  private selecting: boolean;
  private selection: TargetRegion;
  private image: Image;

  @ViewChild("shimmerCanvas") private canvas: ElementRef;
  @ViewChild(TargetClassifierComponent) private classifierWindow: TargetClassifierComponent;
  constructor(private service: ImagesService) {
    this.locked = false;
    this.selecting = false;
    this.selection = null;
  }

  ngAfterViewInit() {
    this.context = this.canvas.nativeElement.getContext('2d');
    this.update();
  }

  update() {
    this.service.getNext().subscribe(
        (image: Image) => {
            this.image = image;
            this.imageElement = new (window as any).Image();
            this.imageElement.src = this.service.getImageURL(image);
            this.imageElement.onload = () => {
                this.render();
            }
        },
        (error: any) => {
            alert("Failed to load next image: " + error.message);
            console.error(error);
        }
    );
  }

  /**
   * Render the image and all target regions
   */
  private render() {
    let height = this.canvas.nativeElement.height = window.innerHeight;
    let width = this.canvas.nativeElement.width = window.innerWidth;
    this.context.clearRect(0, 0, width, height);

    this.context.drawImage(this.imageElement, 0, 0, width, height);
    this.image.targets.forEach((targetRegion: TargetRegion) => {
        this.renderTargetRegion(targetRegion);
    });
    if(this.selection != null && this.selection.b != null) {
        this.renderTargetRegion(this.selection);
    }
  }

  private renderTargetRegion(targetRegion: TargetRegion) {
    this.context.fillStyle = 'rgba(127, 255, 127, 0.3)';
    var x1 = targetRegion.a.x * (this.canvas.nativeElement.width/this.imageElement.width);
    var y1 = targetRegion.a.y * (this.canvas.nativeElement.height/this.imageElement.height);
    var x2 = targetRegion.b.x * (this.canvas.nativeElement.width/this.imageElement.width);
    var y2 = targetRegion.b.y * (this.canvas.nativeElement.height/this.imageElement.height);
    this.context.fillRect(x1, y1, x2-x1, y2-y1);
  }

  lock() {
    this.locked = true;
  }

  unlock() {
    this.locked = false;
  }

  /****************************** Target Classifier Handlers ******************************/

  targetSubmitted(_: Target) {}

  targetRegionSubmitted(_: TargetRegion) {
    // Ensure this image is up to date
    this.service.getImage(this.image.id).subscribe((image: Image) => {
        this.image = image;
        this.render();
    }, (error) => {
        console.error(error);
    });
  }

  /********************************* Mouse Event Handlers *********************************/

  mouseDown(event) {
    if(this.locked) {
        // Exit if the target classifier window is showing
        return;
    }
    let point = new Point(event.x * (this.imageElement.width/this.canvas.nativeElement.width),
                          event.y * (this.imageElement.height/this.canvas.nativeElement.height));
    this.image.targets.forEach((targetRegion: TargetRegion) => {
        if(targetRegion.contains(point)) {
            this.lock();
            this.service.getTarget(targetRegion.target_id).subscribe((target: Target) => {
                this.classifierWindow.show(this.imageElement, targetRegion, target);
            },
            (error) => {
                console.error(error);
                this.unlock();
            });
            return;
        }
    });
    if(this.locked) {
        // Exit if the target classifier window is showing
        return;
    }
    this.selecting = true;
    this.selection = new TargetRegion(new Point(
            Math.round(event.x * (this.imageElement.width/this.canvas.nativeElement.width)),
            Math.round(event.y * (this.imageElement.height/this.canvas.nativeElement.height))
        ), null, null, this.image.id);
  }

  mouseMove(event) {
    if (!this.selecting) {
        // Exit if an area is not currently being selected
        return;
    }
    this.selection.b = new Point(
        Math.round(event.x * (this.imageElement.width/this.canvas.nativeElement.width)),
        Math.round(event.y * (this.imageElement.height/this.canvas.nativeElement.height))
    );

    this.render();
  }

  mouseUp(event) {
    if(this.locked) {
        // Exit if the target classifier window is showing
        return;
    }
    this.selecting = false;
    this.selection.b = new Point(
        Math.round(event.x * (this.imageElement.width/this.canvas.nativeElement.width)),
        Math.round(event.y * (this.imageElement.height/this.canvas.nativeElement.height))
    );
    if (this.selection.a.delta(this.selection.b) < ImagesComponent.MIN_SELECTION_SIZE) {
        this.selection = null;
        return;
    }
    if (this.selection.a.x > this.selection.b.x) {
        // This ensures a is smaller than b
        let temp = this.selection.a;
        this.selection.a = this.selection.b;
        this.selection.b = temp;
    }

    this.lock();
    this.classifierWindow.show(this.imageElement, this.selection);
    this.render();
    // Clear the selection
    this.selection = null;
  }
}
