package mwm.domain.exceptions.already_exists;

import mwm.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class AddressAlreadyExistsException extends EntityAlreadyExistsException {
public AddressAlreadyExistsException(String message) {
        super(message);
    }
}