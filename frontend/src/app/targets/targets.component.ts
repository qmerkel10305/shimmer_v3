import { Component, OnInit, ViewChild } from '@angular/core';
import { TargetsService } from './targets.service';
import { Target } from 'types/target';
import { TargetEditorComponent } from 'app/targets/target-modifers/target-editor/target-editor.component';
import { TargetRow } from 'types/targetRow';
import { TargetRegion } from 'types/targetRegion';
import { filter } from 'rxjs/operators';
import { TargetThumbComponent } from './target-modifers/target-thumb/target-thumb.component';

@Component({
  selector: 'app-targets',
  templateUrl: './targets.component.html',
  styleUrls: ['./targets.component.css']
})
export class TargetsComponent implements OnInit {
  public rows: TargetRow[] = [];

  showTargetFields = true;

  @ViewChild(TargetEditorComponent) private editWindow: TargetEditorComponent;
  @ViewChild(TargetThumbComponent) private thumbWindow: TargetThumbComponent;
  constructor(private service: TargetsService) {
  }

  ngOnInit() {
    this.refresh();
  }

  async merge() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filtered.length >= 2) {
      const targets = [];
      let row = filtered[0];
      for (const i of filtered) {
        if (i.regions.length < row.regions.length) {
          targets.push(i.target.id);
        } else if (row !== i) {
          targets.push(row.target.id);
          row = i;
        }
      }
      await this.service.mergeTargets(row.target.id, targets).toPromise();
      // this.mergeWindow.merge(targets);
    } else {
      alert('Please select at least 2 targets');
    }
    this.refresh();
  }

  edit() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filtered.length === 1) {
      this.editWindow.edit(filtered[0].target);
    } else {
      alert('Please select only 1 target');
    }
  }

  thumb() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filtered.length === 1) {
      this.thumbWindow.thumb(filtered[0].target);
    } else {
      alert('Please select only 1 target');
    }
  }

  async delete() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filter.length > 0 && confirm('Do you want to delete ' + filtered.length + ' targets?')) {
      for (const target of filtered) {
        await this.service.deleteTarget(target.target).toPromise();
      }
    } else {
      alert('Please select at least 1 target');
    }
    this.refresh();
  }

  refresh() {
    this.rows = [];
    this.service.getAllTargets().subscribe((targets: Target[]) => {
      for (const target of targets) {
        this.service.getTargetRegions(target.id).subscribe((regions: TargetRegion[]) => {
          for (let i = 0; i < regions.length; i++) {
            this.service.getShimmerImageID(regions[i].image_id).subscribe((image_id: string) => {
              regions[i].image_id = parseInt(image_id, 10);
            });
          }
          this.rows.push(new TargetRow(target, false, regions));
        });
      }
    }, (error) => {
      console.error(error);
    });
  }
}
