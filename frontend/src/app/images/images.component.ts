import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { switchMap } from 'rxjs/operators';

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
  public flightString: String;


  private xDifference: number;
  private yDifference: number;
  private canvasElement: HTMLCanvasElement;
  private imageHeight: number;
  private imageWidth: number;

  @ViewChild('shimmerCanvas') private canvas: ElementRef;
  @ViewChild(TargetClassifierComponent) private classifierWindow: TargetClassifierComponent;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: ImagesService
  ) {
    this.locked = false;
    this.selecting = false;
    this.selection = null;
  }

  ngAfterViewInit() {
    this.service.getFlightID().subscribe(
      (temp: String) => {
        this.flightString = 'Flight ID: ' + temp;
      },
      (error: any) => {
        alert('Failed to get flight id: ' + error.message);
        console.error(error);
      }
    );
    this.canvasElement = this.canvas.nativeElement;
    this.context = this.canvas.nativeElement.getContext('2d');
    this.route.paramMap.subscribe(
      (params: ParamMap) => {
        const id: string = params.get('id');
        if (id === "next") {
          this.loadNextImage();
          return;
        }
        this.service.getImage(parseInt(id)).subscribe(
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
            alert('Failed to load image: ' + error.message);
            console.error(error);
          }
        )
      }
    );
  }

  /**
   * Redirect to the next image from the server
   */
  private loadNextImage() {
    this.service.getNext().subscribe(
      (image: Image) => {
        this.router.navigate([`/images/${image.id}`]);
      },
      (error: any) => {
        alert('Failed to load next image: ' + error.message);
        console.error(error);
      }
    );
  }

  /**
   * Render the image and all target regions.  Scales the image to preserve aspect ratio
   */
  private render() {
    // Set image height and width and canvasElement height and width to the height and width of the window
    // Image height and width will be reassigned later
    this.imageHeight = this.canvasElement.height = window.innerHeight;
    this.imageWidth = this.canvasElement.width = window.innerWidth;

    this.context.clearRect(0, 0, this.imageWidth, this.imageHeight);

    // Calculates image and widow ratio to determine which dimension (height or width) we need to scale
    const imageRatio = this.imageElement.width / this.imageElement.height;
    const windowRatio = this.imageWidth / this.imageHeight;

    // If the image has a larger width than height then reset the width
    if (imageRatio < windowRatio) {
      this.imageWidth = window.innerHeight * imageRatio;
    } else { // If the image has a larger height than width then reset the height
      this.imageHeight = window.innerWidth / imageRatio;
    }

    // Calculate the offset needed for each dimension
    this.xDifference = (window.innerWidth - this.imageWidth) / 2;
    this.yDifference = (window.innerHeight - this.imageHeight) / 2;

    // Function that draws the image with offset and dimensions
    this.context.drawImage(this.imageElement, this.xDifference, this.yDifference, this.imageWidth, this.imageHeight);
    // Render stored targets onto image
    this.image.targets.forEach((targetRegion: TargetRegion) => {
      this.renderTargetRegion(targetRegion);
    });
    if (this.selection != null && this.selection.b != null) {
      this.renderTargetRegion(this.selection);
    }
  }

  /**
   * Render target regions along scaled picture
  */
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

    // Doesn't allow targets to be drawn in regions where the picture isn't when mouse is clicked
    if (event.x < this.xDifference || event.y < this.yDifference ||
      event.x > this.xDifference + this.imageWidth || event.y > this.yDifference + this.imageHeight) {
      return;
    }
    // translate coordinates from window to canvas to scaled picture
    const point = new Point(Math.round((event.x - this.xDifference) * (this.imageElement.width / this.imageWidth)),
      Math.round((event.y - this.yDifference) * (this.imageElement.height / this.imageHeight)));

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
    // Define initial selection point for potential target region
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

    let x: number, y: number;

    // Checks to see if x coordinate is greater than image width plus offset, if so sets x to edge of image
    if (event.x > this.imageWidth + this.xDifference) {
      x = this.imageWidth + this.xDifference;
    } else if (event.x < this.xDifference) { // Checks to see if x coordinate is in the offset, if so sets x to beginning of image
      x = this.xDifference;
    } else { // Valid x coordinate
      x = event.x;
    }

    // Checks to see if y coordinate is greater than image height plus offset, if so sets y to edge of image
    if (event.y > this.imageHeight + this.yDifference) {
      y = this.imageHeight + this.yDifference;
    } else if (event.y < this.yDifference) { // Checks to see if y coordinate is in the offset, if so sets y to beginning of image
      y = this.yDifference;
    } else { // Valid y coordinate
      y = event.y;
    }

    // Intermediate point when mouse is moving
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
      // Exit if an area is not currently being selected
      return;
    }

    let x: number, y: number;

    // Checks to see if x coordinate is greater than image width plus offset, if so sets x to edge of image
    if (event.x > this.imageWidth + this.xDifference) {
      x = this.imageWidth + this.xDifference;
    } else if (event.x < this.xDifference) { // Checks to see if x coordinate is in the offset, if so sets x to beginning of image
      x = this.xDifference;
    } else { // Valid x coordinate
      x = event.x;
    }

    // Checks to see if y coordinate is greater than image height plus offset, if so sets y to edge of image
    if (event.y > this.imageHeight + this.yDifference) {
      y = this.imageHeight + this.yDifference;
    } else if (event.y < this.yDifference) { // Checks to see if y coordinate is in the offset, if so sets y to beginning of image
      y = this.yDifference;
    } else { // Valid y coordinate
      y = event.y;
    }

    this.selecting = false;
    // Final point of the target region
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
      const x_temp = this.selection.a.x;
      this.selection.a.x = this.selection.b.x;
      this.selection.b.x = x_temp;
    }
    if (this.selection.a.y > this.selection.b.y) {
      // This ensures a is smaller than b
      const y_temp = this.selection.a.y;
      this.selection.a.y = this.selection.b.y;
      this.selection.b.y = y_temp;
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
    switch (event.key) {
      case 'Enter': // Enter Key
        this.loadNextImage();
        break;
      case 'ArrowLeft': // Left Arrow Key
        this.router.navigate([`/images/${this.image.id - 1}`]);
        break;
      case 'ArrowUp': // Up Arrow Key
        const id = parseInt(prompt('Image id number?', '0'), 10);
        this.router.navigate([`/images/${id}`]);
        break;
      case 'ArrowRight': // Right Arrow Key
        this.router.navigate([`/images/${this.image.id + 1}`]);
        break;
    }
  }
}
