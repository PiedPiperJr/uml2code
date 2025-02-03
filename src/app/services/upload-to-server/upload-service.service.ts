import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../@core/environnment';
import { ServerInput } from '../../models/server-input';

export interface UploadProgress {
  progress: number;
  downloadUrl?: string;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class UploadServiceService {
  private readonly API_URL = `${environment.apiUrl}/process`;

  constructor(private http: HttpClient) {}

  uploadFileWithProgress(file: File, serverInput: ServerInput): Observable<UploadProgress> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('data', JSON.stringify(serverInput));

    return this.http.post(this.API_URL, formData, {
      reportProgress: true,
      observe: 'events',
      responseType: 'blob'
    }).pipe(
      map((event: HttpEvent<Blob>): UploadProgress => {
        switch (event.type) {
          case HttpEventType.UploadProgress:
            const progress = event.total ? Math.round(100 * event.loaded / event.total) : 0;
            return { progress };
            
          case HttpEventType.Response:
            if (event instanceof HttpResponse && event.body) {
              const blob = new Blob([event.body], { type: 'application/zip' });
              const downloadUrl = window.URL.createObjectURL(blob);
              return { progress: 100, downloadUrl };
            }
            return { progress: 100 };
            
          default:
            return { progress: 0 };
        }
      })
    );
  }
}