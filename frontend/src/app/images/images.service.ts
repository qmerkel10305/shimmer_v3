import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import {map} from 'rxjs/operators';

import { environment } from 'environments/environment';

import { Image } from 'types/image';
import { Target } from 'types/target';
import { Point } from 'types/point';
import { TargetRegion } from 'types/targetRegion';

@Injectable({
  providedIn: 'root'
})
export class ImagesService {
  constructor(private http: HttpClient) { }

  getNext(): Observable<Image> {
    return this.http.get(`${environment.api_url}/next`).pipe(map(this._deserializeImage));
  }

  getImage(id: number): Observable<Image> {
    return this.http.get(`${environment.api_url}/image/${id}`).pipe(map(this._deserializeImage));
  }

  getImageURL(image: Image): string {
    return `${environment.api_url}/image/${image.id}/img.jpg`;
  }

  getTarget(id: number): Observable<Target> {
    return this.http.get<Target>(`${environment.api_url}/target/${id}`);
  }

  createTarget(image: Image, target: Target, targetRegion: TargetRegion): Observable<any> {
    let submit_object: any = {
      "target": target,
      "target_region": targetRegion
    }
    return this.http.post<any>(`${environment.api_url}/image/${image.id}/target`, submit_object);
  }

  putTarget(target: Target): Observable<Target> {
    return this.http.put<Target>(`${environment.api_url}/target/${target.id}`, target);
  }

  postTargetRegion(targetRegion: TargetRegion): Observable<TargetRegion> {
    return this.http.post<TargetRegion>(`${environment.api_url}/image/${targetRegion.image_id}/targets`, targetRegion);
  }

  deleteTargetRegion(targetRegion: TargetRegion): Observable<TargetRegion> {
    return this.http.delete<TargetRegion>(`${environment.api_url}/image/${targetRegion.image_id}/targets/${targetRegion.target_id}`);
  }

  _deserializeImage(raw_image: Image): Image {
    for (let i = 0; i < raw_image.targets.length; i++) {
      raw_image.targets[i] = new TargetRegion(
        new Point(raw_image.targets[i].a.x, raw_image.targets[i].a.y),
        new Point(raw_image.targets[i].b.x, raw_image.targets[i].b.y),
        raw_image.targets[i].target_id,
        raw_image.targets[i].image_id
      );
    }
    return raw_image;
  }
}
