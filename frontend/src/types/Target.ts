export interface Target {
  thumb: string;
  id: number;
  type: string;
  regions: TargetRegion[];
  letter?: string;
  letter_color?: string;
  shape?: string;
  shape_color?: string;
  orientation?: number;
  notes?: string;
}

export interface TargetRegion {
  top_left: Point;
  bottom_right: Point;
  target_id: number;
  image_id: number;
  id: number;
}

export interface Point {
  x: number;
  y: number;
}
