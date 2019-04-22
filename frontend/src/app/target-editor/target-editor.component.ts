import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { TargetsService } from 'app/targets/targets.service';
import { ImagesService } from 'app/images/images.service';
import { Target } from 'types/target';

@Component({
    selector: 'app-target-editor',
    templateUrl: './target-editor.component.html',
    styleUrls: ['./target-editor.component.css']
})
export class TargetEditorComponent implements AfterViewInit {
    static readonly SUBMIT_TEXT = 'Submit';
    static readonly UPDATE_TEXT = 'Update';
    static readonly DISCARD_TEXT = 'Discard';
    static readonly DELETE_TEXT = 'Delete';

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
    submitText: string;
    showProtractor = false;

    @ViewChild('editTarget') private content: ElementRef;

    @Output() windowClosed = new EventEmitter<boolean>();

    ngAfterViewInit() {
        this.content.nativeElement.style = 'display: none';
    }

    constructor (private tService: TargetsService, private iService: ImagesService) {
        this.content = null;
        this.submitText = TargetEditorComponent.SUBMIT_TEXT;
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

    update(){
        this.iService.putTarget(this.target).subscribe((target: Target) => {
            this.close();
        }, (error) => {
            console.error(error);
        });
    }

    discard(){
        this.content.nativeElement.style = 'display: none';
        this.resetFields();
    }

    showTargetAligner() {
        this.showProtractor = true;
        console.log("Show Protractor");
    }

    hideTargetAligner() {
        this.showProtractor = false;
    }
}