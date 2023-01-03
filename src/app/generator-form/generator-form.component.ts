import { Component } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

interface GeneratorForm {
  proposalCode: FormControl<string | null>;
}

@Component({
  selector: 'fcg-generator-form',
  templateUrl: './generator-form.component.html',
  styleUrls: ['./generator-form.component.scss'],
})
export class GeneratorFormComponent {
  form: FormGroup<GeneratorForm> = this.fb.group({
    proposalCode: new FormControl('', [Validators.required], []),
  });

  constructor(private fb: FormBuilder) {}
}
