package mwm.domain.exceptions.not_found;

import mwm.domain.exceptions.EntityNotFoundException;

public class PersonNotFoundException extends EntityNotFoundException {
public PersonNotFoundException(String message) {
        super(message);
    }
}