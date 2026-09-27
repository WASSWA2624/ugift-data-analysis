# Register revision status

Date: 27 September 2026

The revised REF register is `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx`. The earlier REF workbook remained open in Excel and was left unchanged.

The revised register contains 225,133 asset rows. Cost entries were completed on 668 rows that previously had no cost. A cell-by-cell comparison found changes only on those rows and their related classification, account and depreciation fields. A focused check passed all 668 cost and amount mirrors, including cost less accumulated depreciation equalling net book value.

The full package validator scanned all 225,133 aligned rows but did not pass. Its quantity-audit input covers only the first 39,197 rows, and it also reports facility-name, provenance and date exceptions. Details are in `validation-report-revised.json`. The focused value checks above passed; the broader source and register exceptions remain for separate reconciliation.
