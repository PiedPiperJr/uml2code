import {UploadedFile} from './uploaded-file';
import {SpringBootFormData} from './spring-boot-form-data';

interface ServerInputBase {
  files : UploadedFile[],
  type : string,
}
export interface SpringBootServerInput extends ServerInputBase {
  type: 'springboot';
  spring_data: SpringBootFormData;
  pomxml_url: string;
}

export interface LaravelServerInput extends ServerInputBase {
  type: 'laravel';
  project_name: string;
}

export type ServerInput = SpringBootServerInput | LaravelServerInput;
