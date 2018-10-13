import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { Image } from 'types/image';

import { environment } from 'environments/environment'

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
}
