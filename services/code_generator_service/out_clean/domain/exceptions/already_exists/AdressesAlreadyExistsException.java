package mwm.domain.exceptions.already_exists;

import mwm.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class AdressesAlreadyExistsException extends EntityAlreadyExistsException {
public AdressesAlreadyExistsException(String message) {
        super(message);
    }
}