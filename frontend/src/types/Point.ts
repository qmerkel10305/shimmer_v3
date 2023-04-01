export class Point {
  constructor(public x: number, public y: number) {}

  delta(point: Point) {
    return Math.sqrt((this.x - point.x) ** 2 + (this.y - point.y) ** 2);
  }
}
