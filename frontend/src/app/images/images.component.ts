import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ImagesService } from './images.service';

import { Point } from 'types/point';
import { Image } from 'types/image';
import { TargetRegion } from 'types/targetRegion';

import { TargetClassifierComponent } from './target-classifier/target-classifier.component';
import { Target } from 'types/target';

import { HostListener } from '@angular/core';

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
  public imageString: String;

  private xDifference: number;
  private yDifference: number;
  private canvasElement: HTMLCanvasElement;
  private imageHeight: number;
  private imageWidth: number;

  @ViewChild('shimmerCanvas') private canvas: ElementRef;
  @ViewChild(TargetClassifierComponent) private classifierWindow: TargetClassifierComponent;
  constructor(private service: ImagesService) {
    this.locked = false;
    this.selecting = false;
    this.selection = null;
  }

  ngAfterViewInit() {
    this.canvasElement = this.canvas.nativeElement;
    this.context = this.canvas.nativeElement.getContext('2d');
    this.update();
  }

  update() {
    this.service.getNext().subscribe(
      (image: Image) => {
        this.image = image;
        this.imageString = 'Image Id: ' + image.id.toString();
        this.imageElement = new (window as any).Image();
        this.imageElement.src = this.service.getImageURL(image);
        this.imageElement.onload = () => {
          this.render();
        };
      },
      (error: any) => {
        alert('Failed to load next image: ' + error.message);
        console.error(error);
      }
    );
  }

  /**
   * Uses the service getImage to subscribe to the selected image
   * @param id the id of the image to get
   */
  getImage(id) {
    id = Math.round(id);
    if (!isNaN(id) && id >= 0) {
      this.service.getImage(id).subscribe(
        (image: Image) => {
          this.image = image;
          this.imageString = 'Image Id: ' + image.id.toString();
          this.imageElement = new (window as any).Image();
          this.imageElement.src = this.service.getImageURL(image);
          this.imageElement.onload = () => {
            this.render();
          };
        },
        (error: any) => {
          alert('Failed to load next image: ' + error.message);
          console.error(error);
        }
      );
    }
  }

  /**
   * Render the image and all target regions
   */
  private render() {
    this.imageHeight = this.canvasElement.height = window.innerHeight;
    this.imageWidth = this.canvasElement.width = window.innerWidth;

    this.context.clearRect(0, 0, this.imageWidth, this.imageHeight);

    const imageRatio = this.imageElement.width / this.imageElement.height;
    const windowRatio = this.imageWidth / this.imageHeight;

    if (imageRatio < windowRatio) {
      this.imageWidth = window.innerHeight * imageRatio;
    } else {
      this.imageHeight = window.innerWidth / imageRatio;
    }

    this.xDifference = (window.innerWidth - this.imageWidth) / 2;
    this.yDifference = (window.innerHeight - this.imageHeight) / 2;

    this.context.drawImage(this.imageElement, this.xDifference, this.yDifference, this.imageWidth, this.imageHeight);
    this.image.targets.forEach((targetRegion: TargetRegion) => {
      this.renderTargetRegion(targetRegion);
    });
    if (this.selection != null && this.selection.b != null) {
      this.renderTargetRegion(this.selection);
    }
  }

  private renderTargetRegion(targetRegion: TargetRegion) {
    this.context.fillStyle = 'rgba(127, 255, 127, 0.3)';
    const x1 = (targetRegion.a.x * (this.imageWidth / this.imageElement.width)) + this.xDifference;
    const y1 = (targetRegion.a.y * (this.imageHeight / this.imageElement.height)) + this.yDifference;
    const x2 = (targetRegion.b.x * (this.imageWidth / this.imageElement.width)) + this.xDifference;
    const y2 = (targetRegion.b.y * (this.imageHeight / this.imageElement.height)) + this.yDifference;
    this.context.fillRect(x1, y1, x2 - x1, y2 - y1);
  }

  lock() {
    this.locked = true;
  }

  unlock() {
    this.locked = false;
  }

  /****************************** Target Classifier Handlers ******************************/

  targetSubmitted(_: Target) { }

  targetRegionSubmitted(_: TargetRegion) {
    // Ensure this image is up to date
    this.service.getImage(this.image.id).subscribe((image: Image) => {
      this.image = image;
      this.render();
    }, (error) => {
      console.error(error);
    });
  }

  targetRegionDeleted(_: TargetRegion) {
    this.service.getImage(this.image.id).subscribe((image: Image) => {
      this.image = image;
      this.render();
    }, (error) => {
      console.error(error);
    });
  }

  /********************************* Mouse Event Handlers *********************************/

  mouseDown(event) {
    if (this.locked) {
      // Exit if the target classifier window is showing
      return;
    }
    if (event.x < this.xDifference || event.y < this.yDifference ||
      event.x > this.xDifference + this.imageWidth || event.y > this.yDifference + this.imageHeight) {
      return;
    }
    // translate coordinates from window to canvas to scaled picture
    const point = new Point(Math.round((event.x - this.xDifference) * (this.imageElement.width / this.imageWidth)),
      Math.round((event.y - this.yDifference) * (this.imageElement.height / this.imageHeight)));
    console.log(JSON.stringify(point));
    this.image.targets.forEach((targetRegion: TargetRegion) => {
      if (targetRegion.contains(point)) {
        this.lock();
        this.service.getTarget(targetRegion.target_id).subscribe((target: Target) => {
          this.classifierWindow.show(this.imageElement, targetRegion, this.image, target);
        },
          (error) => {
            console.error(error);
            this.unlock();
          });
        return;
      }
    });
    if (this.locked) {
      // Exit if the target classifier window is showing
      return;
    }
    this.selecting = true;
    this.selection = new TargetRegion(new Point(
      Math.round((event.x - this.xDifference) * (this.imageElement.width / this.imageWidth)),
      Math.round((event.y - this.yDifference) * (this.imageElement.height / this.imageHeight))
    ), null, null, this.image.id);
  }

  mouseMove(event) {
    if (!this.selecting) {
      // Exit if an area is not currently being selected
      return;
    }

    let x, y;

    if (event.x > this.imageWidth + this.xDifference) {
      x = this.imageWidth + this.xDifference;
    } else if (event.x < this.xDifference) {
      x = this.xDifference;
    } else {
      x = event.x;
    }

    if (event.y > this.imageHeight + this.yDifference) {
      y = this.imageHeight + this.yDifference;
    } else if ( event.y < this.yDifference) {
      y = this.yDifference;
    } else {
      y = event.y;
    }

    this.selection.b = new Point(
      Math.round((x - this.xDifference) * (this.imageElement.width / this.imageWidth)),
      Math.round((y - this.yDifference) * (this.imageElement.height / this.imageHeight))
    );

    this.render();
  }

  mouseUp(event) {
    if (this.locked) {
      // Exit if the target classifier window is showing
      return;
    }
    if (!this.selecting) {
      return;
    }

    let x, y;

    if (event.x > this.imageWidth + this.xDifference) {
      x = this.imageWidth + this.xDifference;
    } else if (event.x < this.xDifference) {
      x = this.xDifference;
    } else {
      x = event.x;
    }

    if (event.y > this.imageHeight + this.yDifference) {
      y = this.imageHeight + this.yDifference;
    } else if ( event.y < this.yDifference) {
      y = this.yDifference;
    } else {
      y = event.y;
    }

    this.selecting = false;
    this.selection.b = new Point(
      Math.round((x - this.xDifference) * (this.imageElement.width / this.imageWidth)),
      Math.round((y - this.yDifference) * (this.imageElement.height / this.imageHeight))
    );

    if (this.selection.a.delta(this.selection.b) < ImagesComponent.MIN_SELECTION_SIZE) {
      this.selection = null;
      return;
    }
    if (this.selection.a.x > this.selection.b.x) {
      // This ensures a is smaller than b
      const temp = this.selection.a;
      this.selection.a = this.selection.b;
      this.selection.b = temp;
    }

    this.lock();
    this.classifierWindow.show(this.imageElement, this.selection, this.image);
    this.render();
    // Clear the selection
    this.selection = null;
  }

  @HostListener('document:keydown', ['$event'])
  keyDown(event: KeyboardEvent) {
    if (this.locked) {
      return;
    }
    switch (event.keyCode) {
      case 13: // Enter Key
        this.update();
        break;
      case 37: // Left Arrow Key
        this.getImage(this.image.id - 1);
        break;
      case 38: // Up Arrow Key
        var id = parseInt(prompt("Image id number?", "0"));
        this.getImage(id);
        break;
      case 39: // Right Arrow Key
        this.getImage(this.image.id + 1);
        break;
    }
  }
}
