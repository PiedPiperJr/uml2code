// spring-boot.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import {lastValueFrom} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SpringBootService {
  constructor(private http: HttpClient) {}

  async generateProject(
    dependencies: string,
    groupId: string,
    artifactId: string,
    name: string,
    description: string,
    javaVersion: number
  ): Promise<Blob> {
    const params = new HttpParams()
      .set('dependencies', dependencies)
      .set('bootVersion', '3.4.1')
      .set('javaVersion', javaVersion.toString())
      .set('groupId', groupId)
      .set('baseDir', name)
      .set('description', description);

    return lastValueFrom(
      this.http.get(`api/pom.xml`, {
        params,
        responseType: 'blob'
      })
    );
  }

  downloadFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
}
