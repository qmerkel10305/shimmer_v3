import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { TargetRegion } from 'types/targetRegion';
import { Target } from 'types/target';

@Component({
    selector: 'app-target-classifier',
    templateUrl: './target-classifier.component.html',
    styleUrls: ['./target-classifier.component.css']
})
export class TargetClassifierComponent implements AfterViewInit{
    @Output() windowClosed = new EventEmitter<boolean>();
    @Output() targetSubmitted = new EventEmitter<Target>();
    @Output() targetRegionSubmitted = new EventEmitter<TargetRegion>();

    @ViewChild("classifyTarget") private content: ElementRef;
    @ViewChild("classifyCanvas") private canvas: ElementRef;

    private context: CanvasRenderingContext2D;
    target: Target;
    targetRegion: TargetRegion;

    constructor() {
        this.content = null;
        this.target = null;
        this.targetRegion = null;
        this.resetFields();
    }

    ngAfterViewInit() {
        this.hide();
        this.context = this.canvas.nativeElement.getContext('2d');
    }

    resetFields() {
        this.target = new Target(null, 0, "A", "blue", "square", "blue", 0, "")
    }

    hide() {
        this.content.nativeElement.style = "display: none";
    }

    show(image: HTMLImageElement, targetRegion: TargetRegion) {
        // Show the window
        this.content.nativeElement.style = "display: absolute";
        // This draws the cropped image region on the top half of the canvas
        this.context.drawImage(image, targetRegion.a.x, targetRegion.a.y,
                                targetRegion.width(), targetRegion.height(),
                                0, 0,
                                this.canvas.nativeElement.width,
                                this.canvas.nativeElement.height/2);
    }
  
    close() {
        this.windowClosed.emit(true);
        this.hide();
        this.targetRegion = null;
        this.resetFields();
    }

    submit() {
        this.targetSubmitted.emit(this.target);
        this.targetRegionSubmitted.emit(this.targetRegion);
        this.close();
    }
}
  