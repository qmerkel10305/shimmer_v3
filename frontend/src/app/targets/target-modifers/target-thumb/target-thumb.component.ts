import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit, HostListener } from '@angular/core';
import { Target } from 'types/target';
import { TargetRegion } from 'types/targetRegion';
import { TargetsService } from 'app/targets/targets.service';


@Component({
    selector: 'app-target-thumb',
    templateUrl: './target-thumb.component.html',
    styleUrls: ['./target-thumb.component.css']
})
export class TargetThumbComponent implements AfterViewInit {

    target: Target;
    regions: TargetRegion[]

    @ViewChild('mergeTargets') private content: ElementRef;

    @Output() windowClosed = new EventEmitter<boolean>();

    constructor (public tService: TargetsService) {
        this.content = null;
    }

    ngAfterViewInit() {
        this.content.nativeElement.style = 'display: none';
    }

    thumb(target: Target) {
        this.content.nativeElement.style = 'display: absolute';
        this.target = target;
        this.tService.getTargetRegions(target.id).subscribe((regions: TargetRegion[]) => {
            this.regions = regions;
        });
    }

    close() {
        this.windowClosed.emit(true);
        this.content.nativeElement.style = 'display: none';
    }

    select(id: number) {
        console.log(id);
    }

    @HostListener('document:keydown', ['$event'])
    keyDown(event: KeyboardEvent) {
        switch (event.key) {
            case 'Escape': // Escape Key
                this.close();
                break;
        }
    }
}
