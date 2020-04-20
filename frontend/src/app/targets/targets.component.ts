import { Component, OnInit, ViewChild } from '@angular/core';
import { TargetsService } from './targets.service';
import { Target } from 'types/target';
import { TargetEditorComponent } from 'app/targets/target-modifers/target-editor/target-editor.component';
import { TargetRow } from 'types/targetRow';
import { TargetRegion } from 'types/targetRegion';
import { filter } from 'rxjs/operators';
import { TargetMergerComponent } from './target-modifers/target-merger/target-merger.component';

@Component({
  selector: 'app-targets',
  templateUrl: './targets.component.html',
  styleUrls: ['./targets.component.css']
})
export class TargetsComponent implements OnInit {
  public rows: TargetRow[] = [];

  showTargetFields = true;

  @ViewChild(TargetEditorComponent) private editWindow: TargetEditorComponent;
  @ViewChild(TargetMergerComponent) private mergeWindow: TargetMergerComponent;
  constructor(private service: TargetsService) {
  }

  ngOnInit() {
    this.refresh();
  }

  merge() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filtered.length >= 2) {
      const targets = [];
      for (const row of filtered) {
        targets.push(row.target);
      }
      this.mergeWindow.merge(targets);
    } else {
      alert('Please select at least 2 targets');
    }
  }

  edit() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filtered.length === 1) {
      this.editWindow.edit(filtered[0].target);
    } else {
      alert('Please select only 1 target');
    }
  }

  async delete() {
    const filtered = this.rows.filter((row: TargetRow) => row.checked === true);
    if (filter.length > 0 && confirm('Do you want to delete ' + filtered.length + ' targets?')) {
    } else {
      alert('Please select at least 1 target');
    }
    for (const target of filtered) {
      await this.service.deleteTarget(target.target).toPromise();
    }
    this.refresh();
  }

  refresh() {
    this.rows = [];
    this.service.getAllTargets().subscribe((targets: Target[]) => {
      for (const target of targets) {
        this.service.getTargetRegions(target.id).subscribe((regions: TargetRegion[]) => {
          this.rows.push(new TargetRow(target, false, regions));
        });
      }
    }, (error) => {
      console.error(error);
    });
  }
}
