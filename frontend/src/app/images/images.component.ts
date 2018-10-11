import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ImagesService } from './images.service';

@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.css']
})
export class ImagesComponent implements AfterViewInit {
  private image: HTMLImageElement;
  private context: CanvasRenderingContext2D;
  private targetSelected: boolean;

  private selecting: boolean;
  private selection: any;

  @ViewChild("shimmerCanvas") private canvas: ElementRef;

  constructor(private service: ImagesService) {
    this.targetSelected = false;

    this.selecting = false;
    this.selection = null;
  }

  ngAfterViewInit() {
    this.context = this.canvas.nativeElement.getContext('2d');
    this.update();
  }

  update() {
    this.service.getNext().subscribe(
        (data: any) => {
            this.image = new (window as any).Image();
            this.image.src = this.service.getImageURL(data["data"]);
            this.image.onload = () => {
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

    this.context.drawImage(this.image, 0, 0, width, height);
    if(this.selection != null && this.selection.b != null) {
        this.context.fillStyle = 'rgba(127, 255, 127, 0.3)';
        this.context.fillRect(
            this.selection.a.x,
            this.selection.a.y,
            this.selection.b.x - this.selection.a.x,
            this.selection.b.y - this.selection.a.y
        );
    }
  }

  /*********** Mouse Event Handlers ***********/

  private mouseDown(event) {
    this.selecting = true;
    this.selection = {
        a: {
            x: event.x,
            y: event.y
        },
        b: null
    }
  }

  private mouseMove(event) {
    if (!this.selecting) {
        return;
    }
    this.selection.b = {
        x: event.x,
        y: event.y
    }

    this.render();
  }

  private mouseUp(event) {
    this.selecting = false;
    this.selection.b = {
        x: event.x,
        y: event.y
    }

    if (this.selection.a.x > this.selection.b.x) {
        // This ensures a is smaller than b
        let temp = this.selection.a;
        this.selection.a = this.selection.b;
        this.selection.b = temp;
    }

    this.render();
    this.targetSelected = true;
  }
}
