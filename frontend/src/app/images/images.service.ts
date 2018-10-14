import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { environment } from 'environments/environment'

import { Image } from 'types/image';
import { Target } from 'types/target';
import { TargetRegion } from 'types/targetRegion';

@Injectable({
  providedIn: 'root'
})
export class ImagesService {
  constructor(private http: HttpClient) { }

  getNext() {
    return this.http.get<Image>(environment.api_url + "/next");
  }

  getImageURL(image: Image) {
    return `${environment.api_url}/image/${image.id}/img.jpg`;
  }

  postTarget(target: Target) {
    this.http.post(environment.api_url + "/target", target);
  }

  postTargetRegion(targetRegion: TargetRegion) {
    this.http.post(`${environment.api_url}/image/${targetRegion.image_id}/target`, targetRegion);
  }
}
