import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit } from '@angular/core';

@Component({
    selector: 'app-target-merger',
    templateUrl: './target-merger.component.html',
    styleUrls: ['./target-merger.component.css']
})
export class TargetMergerComponent implements AfterViewInit {

    @ViewChild('mergeTargets') private content: ElementRef;

    @Output() windowClosed = new EventEmitter<boolean>();

    ngAfterViewInit(): void {
        this.content.nativeElement.style = 'display: none';
    }
    
}