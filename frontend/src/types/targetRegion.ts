import { Point } from './point';

export class TargetRegion {
    constructor(public a: Point, public b: Point, public target_id: number) {}

    width() {
        return this.b.x - this.a.x;
    }

    height() {
        return this.b.y - this.a.y;
    }
}