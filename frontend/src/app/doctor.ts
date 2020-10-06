import { Specialty } from './specialty';

export interface Doctor {
    _id: number;
    name: string;
    crm: number;
    email: string;
    phone: string;
    specialty: Specialty;
}
