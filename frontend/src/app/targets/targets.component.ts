import { Component, OnInit, ViewChild } from "@angular/core";
import { TargetsService } from "./targets.service";
import { Target } from 'types/target';
import { TargetEditorComponent } from "app/targets/target-modifers/target-editor/target-editor.component";
import { TargetRow } from "types/targetRow";
import { filter } from "rxjs/operators";

@Component({
  selector: "app-targets",
  templateUrl: "./targets.component.html",
  styleUrls: ["./targets.component.css"]
})
export class TargetsComponent implements OnInit {
  public rows: TargetRow[] = [];

  showTargetFields = true;

  @ViewChild(TargetEditorComponent) private classifierWindow: TargetEditorComponent;
  constructor(private service: TargetsService) {
    service.getAllTargets().subscribe((targets: Target[]) => {
      for(let target of targets){
        this.rows.push(new TargetRow(target, false, false));
      }
      this.showIf();
    }, (error) => {
      console.error(error);
    });
  }
// Pull all targets in constructor
// NgFor to iterate the file
  ngOnInit() {
  }

  showIf(){
    for(let row of this.rows) {
      if(Number(row.target.target_type) === 3){
        row.showCharacteristics = false;
      } else{
        row.showCharacteristics = true;
      }
    }
  }

  merge(){
    var filtered = this.rows.filter((row: TargetRow) => row.isChecked === true);
    if(filtered.length > 2){
    }
    else {
      alert("Please select atleast 2 targets");
    }
  }

  edit(){
    var filtered = this.rows.filter((row: TargetRow) => row.isChecked === true);
    if(filtered.length === 1){
      this.classifierWindow.edit(filtered[0].target);
    }
    else{
      alert("Please select only 1 target");
    }
  }

  delete(){
    var filtered = this.rows.filter((row: TargetRow) => row.isChecked === true);
    if(filter.length > 0 && confirm("Do you want to delete " + filtered.length + " targets?")) {
    }
    else{
      alert("Please select atleast 1 target");
    }
  }

  refresh(){
    window.location.reload();
  }
}
