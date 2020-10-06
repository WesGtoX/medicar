import { Doctor } from './doctor';

export interface Agenda {
    _id: number;
    doctor: Doctor;
    day: string;
    schedule: Array<string>;
}
