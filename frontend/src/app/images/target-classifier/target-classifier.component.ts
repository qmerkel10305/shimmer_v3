import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { TargetRegion } from 'types/targetRegion';
import { Target } from 'types/target';
import { ImagesService } from '../images.service';

@Component({
    selector: 'app-target-classifier',
    templateUrl: './target-classifier.component.html',
    styleUrls: ['./target-classifier.component.css']
})
export class TargetClassifierComponent implements AfterViewInit {
    static readonly SUBMIT_TEXT = 'Submit';
    static readonly UPDATE_TEXT = 'Update';
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

    showTargetFields = true;

    @Output() windowClosed = new EventEmitter<boolean>();
    @Output() targetSubmitted = new EventEmitter<Target>();
    @Output() targetRegionSubmitted = new EventEmitter<TargetRegion>();
    @Output() targetRegionDeleted = new EventEmitter<number>();

    @ViewChild('classifyTarget') private content: ElementRef;
    @ViewChild('classifyCanvas') private canvas: ElementRef;

    private context: CanvasRenderingContext2D;
    target: Target;
    targetRegion: TargetRegion;



    /** Text that shows on the submit button */
    submitText: string;
    /** Index of the current target region (used to delete it) */
    private targetRegionIndex: number;

    constructor(private service: ImagesService) {
        this.content = null;
        this.submitText = TargetClassifierComponent.SUBMIT_TEXT;
        this.resetFields();
    }

    ngAfterViewInit() {
        this.hide();
        this.context = this.canvas.nativeElement.getContext('2d');
    }

    resetFields() {
        this.target = new Target(null, 0, 'A', 'blue', 'square', 'blue', 0, '');
        this.targetRegion = new TargetRegion(null, null, -1, -1);
        this.targetRegionIndex = -1;
    }

    resetDisplay() {
        const height = this.canvas.nativeElement.height;
        const width = this.canvas.nativeElement.width;
        this.context.clearRect(0, 0, width, height);
    }

    hide() {
        this.content.nativeElement.style = 'display: none';
    }

    onChange() {
        if (Number(this.target.target_type) === 3) {
            this.showTargetFields = false;
        } else {
            this.showTargetFields = true;
        }
    }

    /**
     * Show the target classifier
     *
     * If target is present, targetRegionIndex must also be present
     * @param image The Image object to render from
     * @param targetRegion The target region to crop
     * @param target (Optional) The target to display
     * @param targetRegionIndex (Optional) The index of the target region being viewed
     */
    show(image: HTMLImageElement, targetRegion: TargetRegion, target?: Target, targetRegionIndex?: number) {
        this.resetFields();
        this.resetDisplay();
        // Show the window
        this.content.nativeElement.style = 'display: absolute';
        // This draws the cropped image region on the top half of the canvas
        this.context.drawImage(image, targetRegion.a.x, targetRegion.a.y,
                                targetRegion.width(), targetRegion.height(),
                                0, 0,
                                this.canvas.nativeElement.width,
                                this.canvas.nativeElement.height / 2);
        this.targetRegion = targetRegion;

        if (target) {
            this.target = target;
            this.targetRegionIndex = targetRegionIndex;
            this.submitText = TargetClassifierComponent.UPDATE_TEXT;
        } else {
            this.submitText = TargetClassifierComponent.SUBMIT_TEXT;
        }
    }

    close() {
        this.windowClosed.emit(true);
        this.hide();
        this.resetFields();
    }

    submit() {
        if (this.target.id === null) {
            this.service.postTarget(this.target).subscribe((target: Target) => {
                this.targetSubmitted.emit(target);
                this.targetRegion.target_id = target.id;
                if (this.targetRegionIndex === -1) {
                    this.service.postTargetRegion(this.targetRegion).subscribe((targetRegion: TargetRegion) => {
                        this.targetRegionSubmitted.emit(targetRegion);
                        this.close();
                    }, (error) => {
                        console.error(error);
                    });
                }
            }, (error) => {
                console.error(error);
            });
        } else {
             this.service.putTarget(this.target).subscribe((target: Target) => {
                this.targetSubmitted.emit(target);
                this.close();
            }, (error) => {
                console.error(error);
             });
        }
    }

    discard() {
        this.targetRegionDeleted.emit(this.targetRegionIndex);
        this.close();
    }
}
