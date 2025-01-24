package org.enspy.4gi.domain.exceptions.not_found;

import org.enspy.4gi.domain.exceptions.EntityNotFoundException;

public class AddressNotFoundException extends EntityNotFoundException {
public AddressNotFoundException(String message) {
        super(message);
    }
}