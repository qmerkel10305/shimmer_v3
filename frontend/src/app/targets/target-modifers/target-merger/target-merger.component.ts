import { Component, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { Target } from 'types/target';
import { TargetsService } from 'app/targets/targets.service';


@Component({
    selector: 'app-target-merger',
    templateUrl: './target-merger.component.html',
    styleUrls: ['./target-merger.component.css']
})
export class TargetMergerComponent implements AfterViewInit {

    targets: Target[];

    @ViewChild('mergeTargets') private content: ElementRef;

    @Output() windowClosed = new EventEmitter<boolean>();

    constructor (public tService: TargetsService) {
        this.content = null;
    }

    ngAfterViewInit() {
        this.content.nativeElement.style = 'display: none';
    }

    merge(targets: Target[]) {
        this.content.nativeElement.style = 'display: absolute';
        this.targets = targets;
    }

    close(){
        this.windowClosed.emit(true);
        this.content.nativeElement.style = 'display: none';
    }
    
    select(id: number) {
        var temp : number[] = [];
        for(let target of this.targets) {
            if(target.id != id){
                temp.push(target.id);
            }
        }
        this.tService.mergeTargets(id, temp).subscribe((target: Target) => {
            console.log(target);
            this.close();
        });
    }
}