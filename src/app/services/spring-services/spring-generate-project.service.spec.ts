import { TestBed } from '@angular/core/testing';

import { SpringBootService } from './spring-generate-project.service';

describe('SpringGenerateProjectService', () => {
  let service: SpringBootService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpringBootService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
