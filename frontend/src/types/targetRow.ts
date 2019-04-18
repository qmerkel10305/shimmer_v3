import { Target } from "./target";

export class TargetRow {
    constructor(public target: Target, public checked: boolean, public showCharacteristics: boolean) {}
}