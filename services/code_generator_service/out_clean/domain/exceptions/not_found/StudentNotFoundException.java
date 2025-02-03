package mwm.domain.exceptions.not_found;

import mwm.domain.exceptions.EntityNotFoundException;

public class StudentNotFoundException extends EntityNotFoundException {
public StudentNotFoundException(String message) {
        super(message);
    }
}