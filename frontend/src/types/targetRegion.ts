import { Point } from './point';

export class TargetRegion {
    constructor(public a: Point, public b: Point, public target_id: number, public image_id: number) {}

    width() {
        return this.b.x - this.a.x;
    }

    height() {
        return this.b.y - this.a.y;
    }

    contains(p: Point) {
        return ((this.a.x < p.x && p.x < this.b.x) && (this.a.y < p.y && p.y < this.b.y))
    }
}