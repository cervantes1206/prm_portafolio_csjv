<?php
declare(strict_types=1);

namespace App\Infrastructure\Pdf;

use Mpdf\Mpdf;

final class PdfGeneratorMPDF
{
    public function htmlToPdf(string $html): string
    {
        $mpdf = new Mpdf(['tempDir' => sys_get_temp_dir()]);
        $mpdf->WriteHTML($html);
        return $mpdf->Output('', 'S');
    }
}
