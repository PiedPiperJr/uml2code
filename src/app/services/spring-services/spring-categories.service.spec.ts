import { TestBed } from '@angular/core/testing';

import { SpringCategoriesService } from './spring-categories.service';

describe('SpringCategoriesService', () => {
  let service: SpringCategoriesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpringCategoriesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
