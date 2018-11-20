import { Component, OnInit } from "@angular/core";
import { TargetsService } from "./targets.service";
import { Target } from 'types/target';

@Component({
  selector: "app-targets",
  templateUrl: "./targets.component.html",
  styleUrls: ["./targets.component.css"]
})
export class TargetsComponent implements OnInit {
  private targets: Target[];

  showTargetFields = true;

  constructor(private service: TargetsService) {
    service.getAllTargets().subscribe((targets: Target[]) => {
      this.targets=targets;
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
    for(let index = 0; index < this.targets.length; index++) {
      const target = this.targets[index];
      if(Number(target.target_type) === 3){
        this.showTargetFields = false;
      } else{
        this.showTargetFields = true;
      }
    }
  }

}
