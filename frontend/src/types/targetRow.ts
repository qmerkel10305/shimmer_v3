import { Target } from "./target";

export class TargetRow {
    public showCharacteristics: boolean;

    constructor(public target: Target, public checked: boolean) {
        if(Number(this.target.target_type) === 3) {
            this.showCharacteristics = false;
        }
        else {
            this.showCharacteristics = true;
        }
    }
}