import type { Point } from "./Point";

export class TargetRegion {
  constructor(
    public top_left: Point,
    public bottom_right: Point,
    public image_id: number,
    public target_id?: number,
    public id?: number
  ) {}

  width() {
    return this.bottom_right.x - this.top_left.x;
  }

  height() {
    return this.bottom_right.y - this.top_left.y;
  }

  contains(p: Point) {
    return (
      this.top_left.x < p.x &&
      p.x < this.bottom_right.x &&
      this.top_left.y < p.y &&
      p.y < this.bottom_right.y
    );
  }
}
