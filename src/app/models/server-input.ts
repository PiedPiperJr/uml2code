import {UploadedFile} from './uploaded-file';
import {SpringBootFormData} from './spring-boot-form-data';

export interface ServerInput {
  files : UploadedFile[],
  type : string,
  params : SpringBootFormData | string,
}
