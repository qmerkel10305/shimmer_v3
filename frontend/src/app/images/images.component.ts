import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ImagesService } from './images.service';

import { Point } from 'types/point';
import { Image } from 'types/image';
import { TargetRegion } from 'types/targetRegion';

import { TargetClassifierComponent } from './target-classifier/target-classifier.component';

@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.css']
})
export class ImagesComponent implements AfterViewInit {
  private imageElement: HTMLImageElement;
  private context: CanvasRenderingContext2D;

  private locked: boolean;
  private selecting: boolean;
  private selection: any;
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
            console.log(error);
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
    if(this.selection != null && this.selection.b != null) {
        this.context.fillStyle = 'rgba(127, 255, 127, 0.3)';
        var x1 = this.selection.a.x * (this.canvas.nativeElement.width/this.imageElement.width);
        var y1 = this.selection.a.y * (this.canvas.nativeElement.height/this.imageElement.height);
        var x2 = this.selection.b.x * (this.canvas.nativeElement.width/this.imageElement.width);
        var y2 = this.selection.b.y * (this.canvas.nativeElement.height/this.imageElement.height);
        this.context.fillRect(x1, y1, x2-x1, y2-y1);
    }
  }

  lock() {
    this.locked = true;
  }

  unlock() {
    this.locked = false;
  }

  /*********** Mouse Event Handlers ***********/

  private mouseDown(event) {
    if(this.locked) {
        // Exit if the target classifier window is showing
        return;
    }
    this.selecting = true;
    this.selection = {
        a: new Point(
            Math.round(event.x * (this.imageElement.width/this.canvas.nativeElement.width)),
            Math.round(event.y * (this.imageElement.height/this.canvas.nativeElement.height))
        ),
        b: null
    }
  }

  private mouseMove(event) {
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

  private mouseUp(event) {
    if(this.locked) {
        // Exit if the target classifier window is showing
        return;
    }
    this.selecting = false;
    this.selection.b = new Point(
        Math.round(event.x * (this.imageElement.width/this.canvas.nativeElement.width)),
        Math.round(event.y * (this.imageElement.height/this.canvas.nativeElement.height))
    );

    if (this.selection.a.x > this.selection.b.x) {
        // This ensures a is smaller than b
        let temp = this.selection.a;
        this.selection.a = this.selection.b;
        this.selection.b = temp;
    }

    this.lock();
    this.classifierWindow.show(this.imageElement, new TargetRegion(this.selection.a, this.selection.b, null, this.image.id));
    this.render();
  }
}
