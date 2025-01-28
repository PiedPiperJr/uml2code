import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {lastValueFrom} from 'rxjs';
import {environment} from '../../@core/environnment';

@Injectable({
  providedIn: 'root'
})
export class UploadServiceService {
  private readonly API_URL = `${environment.apiUrl}/process`;

  constructor(private http: HttpClient) {}

  async uploadFile(file: File): Promise<Blob> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await lastValueFrom(
      this.http.post(this.API_URL, formData, {
        reportProgress: true,
        observe: 'response',
        responseType: 'blob'
      })
    );

    if (!response.body) {
      throw new Error('No response body received');
    }

    return response.body;
  }

  getUploadProgress(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(this.API_URL, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }

}
