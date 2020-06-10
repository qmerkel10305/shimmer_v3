import { Target } from './target';
import { TargetRegion } from './targetRegion';

export class TargetRow {
    public showCharacteristics: boolean;

    constructor(public target: Target, public checked: boolean, public regions: TargetRegion[]) {
        if (Number(this.target.target_type) === 3) {
            this.showCharacteristics = false;
        } else {
            this.showCharacteristics = true;
        }
    }
}
