import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ImagesService } from './images.service';

@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.css']
})
export class ImagesComponent implements AfterViewInit {
  private service: ImagesService;
  private image: HTMLImageElement;
  private context: CanvasRenderingContext2D;

  @ViewChild("shimmerCanvas") private canvas: ElementRef;

  constructor(imagesService: ImagesService) {
    this.service = imagesService;
  }

  ngAfterViewInit() {
    this.context = this.canvas.nativeElement.getContext('2d');
    this.update();
  }

  update() {
    let height = this.canvas.nativeElement.height = window.innerHeight;
    let width = this.canvas.nativeElement.width = window.innerWidth;
    this.service.getNext().subscribe(
        (data: any) => {
            this.image = new (window as any).Image();
            this.image.src = this.service.getImageURL(data["data"]);
            this.image.onload = () => {
                this.context.drawImage(this.image, 0, 0, width, height);
            }
        },
        (error: any) => {
            alert("Failed to load next image: " + error.message);
            console.log(error);
        }
    );
  }
}
