package mwm.domain.exceptions.already_exists;

import mwm.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class PersonAlreadyExistsException extends EntityAlreadyExistsException {
public PersonAlreadyExistsException(String message) {
        super(message);
    }
}