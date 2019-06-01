import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';

import { Observable } from 'rxjs';
import { environment } from 'environments/environment';

import { Target } from 'types/target';

@Injectable({
  providedIn: 'root'
})
export class TargetsService {

  constructor(private http: HttpClient) { }

  getTarget(id: number): Observable<Target> {
    return this.http.get<Target>(`${environment.api_url}/target/${id}`);
  }

  getAllTargets(): Observable<Target[]> {
    return this.http.get<Target[]>(`${environment.api_url}/target/`);
  }

  getThumbnailURL(id: number){
    return `${environment.api_url}/target/${id}/thumb.jpg`;
  }
}