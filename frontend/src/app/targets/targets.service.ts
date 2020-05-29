import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';

import { Observable } from 'rxjs';
import { environment } from 'environments/environment';

import { Target } from 'types/target';
import { TargetRegion } from 'types/targetRegion';

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

  getTargetThumbnailURL(id: number) {
    return `${environment.api_url}/target/${id}/thumb.jpg`;
  }

  getRegionThumbnailURL(target_id: number, region_id: number) {
    return `${environment.api_url}/target/${target_id}/regions/${region_id}/thumb.jpg`;
  }

  mergeTargets(id: number, targets: number[]): Observable<Target> {
    return this.http.post<Target>(`${environment.api_url}/target/merge/${id}`, targets);
  }

  postTarget(target: Target) {
    return this.http.post<Target>(`${environment.api_url}/target/${target.id}`, target);
  }

  deleteTarget(target: Target): Observable<any> {
    return this.http.delete(`${environment.api_url}/target/${target.id}`);
  }

  getTargetRegions(target_id: number):  Observable<TargetRegion[]> {
    return this.http.get<TargetRegion[]>(`${environment.api_url}/target/${target_id}/regions`);
  }

  getShimmerImageID(data_id: number): Observable<string> {
    return this.http.get<string>(`${environment.api_url}/target/database/image/${data_id}`);
  }
}

