import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CvService } from '../../core/cv.service';
import { CommonModule } from '@angular/common';
import { BehaviorSubject } from 'rxjs';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-cv-classes',
  templateUrl: './cv-classes.component.html',
  styleUrls: ['./cv-classes.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class CvClassesComponent implements OnInit {
  offreId!: number;
  private resultsSubject = new BehaviorSubject<any[]>([]);
  results$ = this.resultsSubject.asObservable();

  loading = true;
  error: string | null = null;

  selectedCVs = new Set<number>();

  constructor(private route: ActivatedRoute, private cvService: CvService) {}

  ngOnInit() {
    this.offreId = Number(this.route.snapshot.paramMap.get('offreId'));
    this.loading = true;
    this.cvService.getCvsClassificationForOffre(this.offreId)
      .pipe(finalize(() => this.loading = false))
      .subscribe({
        next: (res) => {
          const sorted = (res || []).sort(
            (a, b) => (b.score_metier_propose || 0) - (a.score_metier_propose || 0)
          );
          this.resultsSubject.next(sorted);
          this.error = null;
        },
        error: () => {
          this.error = "Erreur lors du chargement des résultats.";
          this.resultsSubject.next([]);
        }
      });
  }

  // Ajoute ou retire un CV sélectionné
  toggleSelect(cvId: number, event: Event) {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) this.selectedCVs.add(cvId);
    else this.selectedCVs.delete(cvId);
  }

  // Appelé au clic sur le bouton principal
  sendTestConfirmation() {
    if (this.selectedCVs.size === 0) {
      alert('Veuillez sélectionner au moins un CV.');
      return;
    }
    this.cvService.sendTestEmail(this.offreId, Array.from(this.selectedCVs))
      .subscribe({
        next: (res) => {
          alert('Email envoyé');
          this.selectedCVs.clear();
        },
        error: (err) => {
          alert("Erreur lors de l'envoi des emails.");
        }
      });
  }
}
