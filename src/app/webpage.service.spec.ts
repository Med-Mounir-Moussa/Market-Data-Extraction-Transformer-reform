import { TestBed, inject } from '@angular/core/testing';

import { WebsiteFormService } from './webpage.service';

describe('WebsiteFormService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WebsiteFormService]
    });
  });

  it('should be created', inject([WebsiteFormService], (service: WebsiteFormService) => {
    expect(service).toBeTruthy();
  }));
});
