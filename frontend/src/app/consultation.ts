import { Doctor } from './doctor'

export interface Consultation {
    _id: number;
    name: string;
    day: string;
    hourly: string;
    scheduling_date: string;
    doctor: Doctor;
}
