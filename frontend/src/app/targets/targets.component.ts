import { Component, OnInit, ViewChild } from "@angular/core";
import { TargetsService } from "./targets.service";
import { Target } from 'types/target';
import { TargetRow } from "types/targetRow";
import { TargetClassifierComponent } from 'app/images/target-classifier/target-classifier.component';

@Component({
  selector: "app-targets",
  templateUrl: "./targets.component.html",
  styleUrls: ["./targets.component.css"]
})
export class TargetsComponent implements OnInit {
  rows: TargetRow[] = [];

  showTargetFields = true;

  @ViewChild(TargetClassifierComponent) private classifierWindow: TargetClassifierComponent;
  constructor(private service: TargetsService) {
    service.getAllTargets().subscribe((targets: Target[]) => {
      for(let target of targets) {
        this.rows.push({
          "target": target,
          "checked": false,
          "showCharacteristics": false
        });
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
    var filteredRow:TargetRow[] = this.rows.filter(row => row.checked);
    if(filteredRow.length < 1){
      alert("Please select atleast one target.");
    }
    else{
      var id:number = parseInt(prompt("Please enter the id of the target with the best thumbnail"));
      console.log(this.rows.filter(row => row.checked));
    }
  }

  delete(){
    var filteredRow:TargetRow[] = this.rows.filter(row => row.checked);
    if(filteredRow.length > 1){
      if(confirm("Are you sure you want to delete this target? THIS CANNOT BE UNDONE!")){

      }
    }
    else if(filteredRow.length === 1) {
      if(confirm("Are you sure you want to delete these targets? THIS CANNOT BE UNDONE!")){

      }
    }
    else{
      alert("Please select atleast one target.");
    }
  }

  edit() {
    var filteredRow:TargetRow[] = this.rows.filter(row => row.checked);
    if(filteredRow.length !== 1){
      alert("Please select one target.");
    }
    else {

    }

  }

}
