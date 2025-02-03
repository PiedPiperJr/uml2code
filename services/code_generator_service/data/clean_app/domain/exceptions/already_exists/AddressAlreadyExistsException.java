package org.enspy.4gi.domain.exceptions.already_exists;

import org.enspy.4gi.domain.exceptions.already_exists.EntityAlreadyExistsException;

public class AddressAlreadyExistsException extends EntityAlreadyExistsException {
public AddressAlreadyExistsException(String message) {
        super(message);
    }
}