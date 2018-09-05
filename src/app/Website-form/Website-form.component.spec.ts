import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WebsiteFormComponent } from './Website-form.component';

describe('WebsiteFormComponent', () => {
  let component: WebsiteFormComponent;
  let fixture: ComponentFixture<WebsiteFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WebsiteFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WebsiteFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
