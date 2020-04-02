import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit, HostListener } from '@angular/core';
import { TargetsService } from 'app/targets/targets.service';
import { ImagesService } from 'app/images/images.service';
import { Target } from 'types/target';
import { Image } from 'types/image';

@Component({
    selector: 'app-target-editor',
    templateUrl: './target-editor.component.html',
    styleUrls: ['./target-editor.component.css']
})
export class TargetEditorComponent implements AfterViewInit {

    ALL_COLORS = [
        'black',
        'blue',
        'brown',
        'gray',
        'green',
        'orange',
        'purple',
        'red',
        'white',
        'yellow',
    ];
    ALL_SHAPES = [
        'circle',
        'semicircle',
        'quarter_circle',
        'square',
        'rectangle',
        'trapezoid',
        'triangle',
        'pentagon',
        'hexagon',
        'octagon',
        'star',
        'cross',
    ];

    target: Target;
    showTargetFields = true;

    private imageElement: HTMLImageElement;
    private canvasElement: HTMLCanvasElement;
    private context: CanvasRenderingContext2D;
    private imageWidth: number;
    private imageHeight: number;
    private offsetX: number;
    private offsetY: number;
    private selecting = false;
    private orig: number;

    @ViewChild('editTarget') private content: ElementRef;
    @ViewChild('protractorCanvas') private canvas: ElementRef;

    @Output() windowClosed = new EventEmitter<boolean>();

    ngAfterViewInit() {
        this.canvasElement = this.canvas.nativeElement;
        this.context = this.canvasElement.getContext('2d');
        this.content.nativeElement.style = 'display: none';

        this.imageElement = new (window as any).Image();
        this.imageElement.src = 'assets/Protractor.png';
        this.imageWidth = this.canvasElement.width = 150;
        this.imageHeight = this.canvasElement.height = 150;
        this.offsetX = this.imageWidth / 2;
        this.offsetY = this.imageHeight / 2;
    }

    constructor (public tService: TargetsService, private iService: ImagesService) {
        this.content = null;
        this.resetFields();
    }

    changeTargetType() {
        if (Number(this.target.target_type) === 3) {
            this.showTargetFields = false;
        } else {
            this.showTargetFields = true;
        }
    }

    edit(target: Target) {
        // Show the window
        this.content.nativeElement.style = 'display: absolute';
        this.target = target;
        this.changeTargetType();
    }

    resetFields() {
        this.target = new Target(null, 0, 'A', 'blue', 'square', 'blue', 0, '');
    }

    close() {
        this.windowClosed.emit(true);
        this.content.nativeElement.style = 'display: none';
        this.resetFields();
    }

    update() {
        this.tService.postTarget(this.target).subscribe((target: Target) => {
            this.close();
        }, (error) => {
            console.error(error);
        });
    }

    discard() {
        this.content.nativeElement.style = 'display: none';
        this.resetFields();
    }

    @HostListener('document:keydown', ['$event'])
    keyDown(event: KeyboardEvent) {
        switch (event.key) {
            case 'Escape': // Escape Key
                this.close();
                break;
        }
    }

    drawProtractor() {
        this.context.clearRect(0, 0, this.imageWidth, this.imageHeight);
        this.context.save();
        this.context.translate(this.offsetX, this.offsetY);
        this.context.rotate(this.target.orientation * Math.PI / 180);
        this.context.drawImage(this.imageElement, -this.offsetX, -this.offsetY,
            this.imageWidth, this.imageHeight);
        this.context.restore();
    }

    /********************************* Mouse Event Handlers *********************************/
    mouseEnter(event: MouseEvent) {
        this.drawProtractor();
    }

    mouseOut(event: MouseEvent) {
        this.context.clearRect(0, 0, this.imageWidth, this.imageHeight);
    }

    mouseDown(event: MouseEvent) {
        this.selecting = true;
        const rect = this.canvasElement.getBoundingClientRect();
        const mouseX = event.clientX - rect.left - this.offsetX;
        const mouseY = event.clientY - rect.top - this.offsetY;
        this.orig = Math.atan2(mouseX, mouseY) * 180 / Math.PI;
    }

    mouseMove(event: MouseEvent) {
        if (!this.selecting) {
            return;
        }
        const rect = this.canvasElement.getBoundingClientRect();
        const mouseX = event.clientX - rect.left - this.offsetX;
        const mouseY = event.clientY - rect.top - this.offsetY;
        const currentAng = Math.atan2(mouseX, mouseY) * 180 / Math.PI;
        this.target.orientation -= currentAng - this.orig;
        this.target.orientation = Math.round(this.target.orientation);
        if (this.target.orientation >= 360) {
            this.target.orientation %= 359;
        } else if (this.target.orientation < 0) {
            this.target.orientation += 360;
        }
        this.orig = currentAng;
        this.drawProtractor();
    }

    mouseUp(event: MouseEvent) {
        this.selecting = false;
    }

}
