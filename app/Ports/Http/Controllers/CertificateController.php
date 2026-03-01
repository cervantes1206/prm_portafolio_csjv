<?php
declare(strict_types=1);

namespace App\Ports\Http\Controllers;

use App\Domain\Portfolio\Repository\PortfolioRepository;
use App\Infrastructure\Pdf\PdfGeneratorMPDF;
use App\Ports\Storage\FileStoragePort;

final class CertificateController
{
    public function __construct(
        private PortfolioRepository $repo,
        private PdfGeneratorMPDF $pdf,
        private FileStoragePort $storage
    ) {}

    public function generate(): void
    {
        $portfolioId = (int)($_GET['portfolio_id'] ?? 0);
        $portfolio = $portfolioId ? $this->repo->findById($portfolioId) : null;

        if (!$portfolio) { http_response_code(404); echo "Portfolio no encontrado"; return; }

        $this->storage->ensureDirs(['certificados', 'exports']);

        $html = "
            <h1>Certificado - Professional Roadmap</h1>
            <p><b>Estudiante:</b> {$portfolio['nombre']}</p>
            <p><b>Grado:</b> {$portfolio['grado']}</p>
            <p><b>Frase:</b> {$portfolio['frase_personal']}</p>
            <hr>
            <p>Este certificado registra evidencia del Portafolio Academico.</p>
        ";

        $pdfBinary = $this->pdf->htmlToPdf($html);
        $filename = 'certificados/certificado_portfolio_' . $portfolioId . '.pdf';
        $fullPath = $this->storage->put($filename, $pdfBinary);

        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['saved' => true, 'path' => $fullPath]);
    }
}
