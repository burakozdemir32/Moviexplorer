import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'truncate'
})
export class TruncatePipe implements PipeTransform {
    transform(value: string, _limit: number): string {
        let limit = _limit;
        let trail = '...';
        if (value == null) {
            return 'No overview.';
        } else {
            return value.length > limit ? value.substring(0, limit) + trail : value;
        }
    }
}